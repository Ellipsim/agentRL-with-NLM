

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b2)
(on b2 b3)
(on b3 b5)
(ontable b4)
(on b5 b8)
(ontable b6)
(on b7 b6)
(ontable b8)
(clear b1)
(clear b4)
(clear b7)
)
(:goal
(and
(on b2 b7)
(on b4 b8)
(on b6 b4)
(on b7 b3)
(on b8 b1))
)
)


