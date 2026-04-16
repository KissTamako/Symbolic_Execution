(set-logic ALL)
; Constraint ID: f12400a0b52b039e
; Generated at: 2026-04-16 11:31:08
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60061)) (False)
(assert (not (= x 60061)))

; Query: ((== x 60062)) (False)
(assert (not (not (= x 60062))))

(check-sat)
(get-model)
