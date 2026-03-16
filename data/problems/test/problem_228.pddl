

(define (problem BW-rand-7)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(on b1 b2)
(ontable b2)
(on b3 b4)
(on b4 b6)
(on b5 b7)
(on b6 b1)
(on b7 b3)
(clear b5)
)
(:goal
(and
(on b1 b6)
(on b2 b1)
(on b5 b4)
(on b7 b5))
)
)


