

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b6)
(on b2 b5)
(on b3 b9)
(on b4 b10)
(ontable b5)
(ontable b6)
(ontable b7)
(on b8 b7)
(on b9 b2)
(on b10 b3)
(clear b1)
(clear b4)
(clear b8)
)
(:goal
(and
(on b1 b4)
(on b2 b7)
(on b4 b2)
(on b7 b6)
(on b8 b5))
)
)


