(set-logic ALL)
; Frontier Constraint ID: c6e60c52082fca4f
; Generated at: 2026-04-16 14:36:25
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 352)) (False)
(assert (not (= x 352)))

; Query: ((== x 353)) (False)
(assert (not (not (= x 353))))

(check-sat)
(get-model)
