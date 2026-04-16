(set-logic ALL)
; Constraint ID: a0fa7d32a9048df1
; Generated at: 2026-04-16 11:00:46
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59620)) (False)
(assert (not (= x 59620)))

; Query: ((== x 59621)) (False)
(assert (not (not (= x 59621))))

(check-sat)
(get-model)
