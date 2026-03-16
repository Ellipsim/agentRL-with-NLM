

(define (problem BW-rand-7)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(on b1 b7)
(on b2 b4)
(on b3 b2)
(ontable b4)
(on b5 b3)
(ontable b6)
(on b7 b5)
(clear b1)
(clear b6)
)
(:goal
(and
(on b2 b7)
(on b3 b1)
(on b4 b3)
(on b6 b2)
(on b7 b5))
)
)


