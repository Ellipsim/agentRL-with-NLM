

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b11)
(on b2 b5)
(ontable b3)
(on b4 b10)
(ontable b5)
(on b6 b3)
(on b7 b9)
(on b8 b6)
(on b9 b8)
(on b10 b12)
(ontable b11)
(on b12 b7)
(clear b1)
(clear b2)
(clear b4)
)
(:goal
(and
(on b1 b3)
(on b2 b4)
(on b3 b9)
(on b4 b10)
(on b6 b12)
(on b9 b8)
(on b10 b11)
(on b11 b5)
(on b12 b7))
)
)


