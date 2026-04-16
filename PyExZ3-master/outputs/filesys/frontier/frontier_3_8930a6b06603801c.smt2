(set-logic ALL)
; Constraint ID: 8930a6b06603801c
; Generated at: 2026-04-16 04:51:40
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59389)) (False)
(assert (not (= x 59389)))

; Query: ((== x 59390)) (False)
(assert (not (not (= x 59390))))

(check-sat)
(get-model)
