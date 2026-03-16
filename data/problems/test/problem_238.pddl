

(define (problem BW-rand-7)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(on b1 b3)
(on b2 b7)
(on b3 b5)
(ontable b4)
(ontable b5)
(on b6 b1)
(ontable b7)
(clear b2)
(clear b4)
(clear b6)
)
(:goal
(and
(on b1 b7)
(on b2 b1)
(on b3 b6)
(on b6 b5))
)
)


