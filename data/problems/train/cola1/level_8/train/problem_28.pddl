

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b10)
(on b2 b1)
(ontable b3)
(ontable b4)
(ontable b5)
(on b6 b4)
(on b7 b6)
(on b8 b7)
(on b9 b5)
(on b10 b3)
(clear b2)
(clear b8)
(clear b9)
)
(:goal
(and
(on b1 b6)
(on b2 b8)
(on b3 b1)
(on b4 b5)
(on b5 b2)
(on b7 b9)
(on b8 b7))
)
)


