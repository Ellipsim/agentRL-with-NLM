

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b8)
(on b2 b6)
(ontable b3)
(ontable b4)
(on b5 b7)
(ontable b6)
(on b7 b1)
(on b8 b3)
(clear b2)
(clear b4)
(clear b5)
)
(:goal
(and
(on b2 b4)
(on b3 b7)
(on b6 b5))
)
)


