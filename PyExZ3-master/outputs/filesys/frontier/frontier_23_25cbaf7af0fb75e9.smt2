(set-logic ALL)
; Constraint ID: 25cbaf7af0fb75e9
; Generated at: 2026-04-16 11:00:46
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59644)) (False)
(assert (not (= x 59644)))

; Query: ((== x 59645)) (False)
(assert (not (not (= x 59645))))

(check-sat)
(get-model)
