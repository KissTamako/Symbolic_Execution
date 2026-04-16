(set-logic ALL)
; Constraint ID: 955ae7eb963a9d7d
; Generated at: 2026-04-16 04:18:59
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59344)) (False)
(assert (not (= x 59344)))

; Query: ((== x 59345)) (False)
(assert (not (not (= x 59345))))

(check-sat)
(get-model)
