

(define (problem BW-rand-7)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(on b1 b2)
(on b2 b6)
(ontable b3)
(on b4 b5)
(ontable b5)
(on b6 b3)
(on b7 b4)
(clear b1)
(clear b7)
)
(:goal
(and
(on b3 b7)
(on b4 b2)
(on b5 b6))
)
)


