(set-logic ALL)
; Executed Path ID: 433c5f848f6b1ef0
; Generated at: 2026-04-17 03:12:51
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: False

(declare-const key Int)

; ((== (^ (+ key (<< key 10)) (>> (+ key (<< key 10)) 6)) (+ key 1))) (False)
(assert (not (= (^ (+ key (<< key 10)) (>> (+ key (<< key 10)) 6)) (+ key 1))))

(check-sat)
(get-model)
