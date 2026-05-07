

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b4)
(on b2 b8)
(ontable b3)
(ontable b4)
(on b5 b2)
(ontable b6)
(on b7 b3)
(on b8 b6)
(clear b1)
(clear b5)
(clear b7)
)
(:goal
(and
(on b2 b3)
(on b3 b6)
(on b4 b2)
(on b5 b4)
(on b7 b5))
)
)


